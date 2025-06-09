import requests
import time
import threading
from collections import Counter
import json
import concurrent.futures

BASE_URL = "http://localhost"

def test_load_balancer():
    """Testa se o load balancer está distribuindo as requisições"""
    print("=== TESTE DE LOAD BALANCER ===")
    url = f"{BASE_URL}/ping"
    responses = []
    
    print("Enviando 100 requisições para /ping via Nginx...")
    
    for i in range(100):
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                host = data.get("host", data.get("instance", "unknown"))
                responses.append(host)
                if i % 20 == 0:
                    print(f"Processadas {i} requisições...")
            else:
                print(f"Erro HTTP: {res.status_code}")
        except Exception as e:
            print(f"Erro na requisição {i}: {e}")
    
    counter = Counter(responses)
    print("\n--- Resultados do Load Balancer ---")
    total = sum(counter.values())
    for host, count in counter.items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{host}: {count} respostas ({percentage:.1f}%)")
    
    if len(counter) >= 2:
        print("✅ Load balancer funcionando!")
    else:
        print("❌ Load balancer NÃO está distribuindo as requisições")
    
    return counter

def test_concurrent_requests():
    """Testa requisições concorrentes"""
    print("\n=== TESTE DE CONCORRÊNCIA ===")
    url = f"{BASE_URL}/ping"
    num_threads = 20
    requests_per_thread = 10
    
    def make_requests(thread_id):
        results = []
        for i in range(requests_per_thread):
            try:
                start_time = time.time()
                res = requests.get(url, timeout=5)
                end_time = time.time()
                
                if res.status_code == 200:
                    data = res.json()
                    results.append({
                        'thread': thread_id,
                        'request': i,
                        'host': data.get("host", data.get("instance", "unknown")),
                        'response_time': end_time - start_time,
                        'success': True
                    })
                else:
                    results.append({
                        'thread': thread_id,
                        'request': i,
                        'success': False,
                        'error': f"HTTP {res.status_code}"
                    })
            except Exception as e:
                results.append({
                    'thread': thread_id,
                    'request': i,
                    'success': False,
                    'error': str(e)
                })
        return results
    
    print(f"Executando {num_threads} threads com {requests_per_thread} requisições cada...")
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_requests, i) for i in range(num_threads)]
        all_results = []
        
        for future in concurrent.futures.as_completed(futures):
            all_results.extend(future.result())
    
    end_time = time.time()
    
    # Análise dos resultados
    successful = [r for r in all_results if r.get('success', False)]
    failed = [r for r in all_results if not r.get('success', False)]
    
    print(f"\n--- Resultados de Concorrência ---")
    print(f"Total de requisições: {len(all_results)}")
    print(f"Sucessos: {len(successful)} ({len(successful)/len(all_results)*100:.1f}%)")
    print(f"Falhas: {len(failed)} ({len(failed)/len(all_results)*100:.1f}%)")
    print(f"Tempo total: {end_time - start_time:.2f}s")
    
    if successful:
        response_times = [r['response_time'] for r in successful]
        print(f"Tempo médio de resposta: {sum(response_times)/len(response_times):.3f}s")
        print(f"Tempo min/max: {min(response_times):.3f}s / {max(response_times):.3f}s")
        
        host_distribution = Counter([r['host'] for r in successful])
        print("Distribuição por instância:")
        for host, count in host_distribution.items():
            print(f"  {host}: {count}")
    
    if failed:
        print("Erros encontrados:")
        error_types = Counter([r.get('error', 'Unknown') for r in failed])
        for error, count in error_types.items():
            print(f"  {error}: {count}")

def test_health_check():
    """Testa se os serviços estão respondendo"""
    print("\n=== TESTE DE SAÚDE ===")
    
    endpoints = [
        f"{BASE_URL}/",
        f"{BASE_URL}/ping",
        "http://localhost:8001/ping",  # Diretamente fastapi1
        "http://localhost:8002/ping",  # Diretamente fastapi2
    ]
    
    for endpoint in endpoints:
        try:
            res = requests.get(endpoint, timeout=5)
            if res.status_code == 200:
                data = res.json()
                print(f"✅ {endpoint}: OK - {data}")
            else:
                print(f"❌ {endpoint}: HTTP {res.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erro - {e}")

def test_stress():
    """Teste de stress básico"""
    print("\n=== TESTE DE STRESS ===")
    url = f"{BASE_URL}/ping"
    
    def stress_worker(worker_id, num_requests):
        successes = 0
        failures = 0
        
        for i in range(num_requests):
            try:
                res = requests.get(url, timeout=2)
                if res.status_code == 200:
                    successes += 1
                else:
                    failures += 1
            except:
                failures += 1
        
        return {'successes': successes, 'failures': failures}
    
    num_workers = 10
    requests_per_worker = 50
    
    print(f"Executando teste de stress: {num_workers} workers, {requests_per_worker} req/worker")
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(stress_worker, i, requests_per_worker) for i in range(num_workers)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    end_time = time.time()
    
    total_successes = sum(r['successes'] for r in results)
    total_failures = sum(r['failures'] for r in results)
    total_requests = total_successes + total_failures
    
    print(f"\n--- Resultados do Teste de Stress ---")
    print(f"Requisições totais: {total_requests}")
    print(f"Sucessos: {total_successes} ({total_successes/total_requests*100:.1f}%)")
    print(f"Falhas: {total_failures} ({total_failures/total_requests*100:.1f}%)")
    print(f"Tempo total: {end_time - start_time:.2f}s")
    print(f"RPS (requisições por segundo): {total_requests/(end_time - start_time):.2f}")

if __name__ == "__main__":
    print("Iniciando suite de testes para backend escalável...\n")
    
    # Aguardar um pouco para garantir que os serviços estejam prontos
    print("Aguardando serviços ficarem prontos...")
    time.sleep(5)
    
    try:
        test_health_check()
        test_load_balancer()
        test_concurrent_requests()
        test_stress()
        
        print("\n🎉 Suite de testes concluída!")
        
    except KeyboardInterrupt:
        print("\n❌ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")